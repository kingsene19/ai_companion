import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:text_to_speech/text_to_speech.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

// import 'package:http/http.dart' as http;

class ChatPage extends StatefulWidget {
  const ChatPage({Key? key}) : super(key: key);

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _tec = TextEditingController();
  ScrollController scrollController = ScrollController();
  bool isRecording = false, isSending = false;

  ObservableList<Map<String, dynamic>> _chatMessages =
      ObservableList<Map<String, dynamic>>();

  // Speech to text
  bool _speechEnabled = false;
  final SpeechToText _speechToText = SpeechToText();
  String _audioMsg = "";

  // Text to speech
  TextToSpeech tts = TextToSpeech();
  String _textMsg = "";
  double volume = 1;
  double rate = 1;
  double pitch = 1;

  @override
  void initState() {
    super.initState();
    _initSpeech();
    speak("Welcome! How may I help you?");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.brown,
          title: Row(
            children: const [
              CircleAvatar(
                backgroundColor: Colors.white,
                child: Image(image: AssetImage('VoiceBot.png'), width: 40),
              ),
              SizedBox(
                width: 10,
              ),
              Text("AI Voice Assistant"),
            ],
          ),
        ),
        body: Stack(children: [
          Container(
            padding: const EdgeInsets.only(bottom: 50),
            decoration: const BoxDecoration(
                image: DecorationImage(
                    image: AssetImage('background.jpeg'), fit: BoxFit.cover)),
            child: StreamBuilder(
              stream: _chatMessages.listStream,
              builder: (context, snapshot) {
                if (snapshot.hasData && snapshot.data != null) {
                  return Column(
                    children: [
                      Expanded(
                        child: ListView.builder(
                          controller: scrollController,
                          reverse: true,
                          itemCount: snapshot.data.length,
                          itemBuilder: (context, index) {
                            return buildItem(
                              snapshot.data[index],
                            );
                          },
                        ),
                      ),
                      const SizedBox(
                        height: 10,
                      ),
                      isSending
                          ? LinearProgressIndicator(
                              backgroundColor: Colors.grey[100],
                              valueColor:
                                  AlwaysStoppedAnimation<Color>(Colors.pink),
                            )
                          : SizedBox(),
                    ],
                  );
                } else {
                  return const Center(
                    child: SizedBox(
                      height: 36,
                      width: 36,
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
                      ),
                    ),
                  );
                }
              },
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              color: Colors.black26,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Container(
                      margin: const EdgeInsets.all(5),
                      padding: const EdgeInsets.fromLTRB(10, 0, 5, 0),
                      decoration: BoxDecoration(
                          color: Colors.grey[200],
                          borderRadius: BorderRadius.circular(20)),
                      child: TextField(
                        decoration: const InputDecoration(
                            hintText: 'Type Here', border: InputBorder.none),
                        controller: _tec,
                      ),
                    ),
                  ),
                  Container(
                      height: 40,
                      margin: const EdgeInsets.fromLTRB(5, 5, 10, 5),
                      decoration: BoxDecoration(boxShadow: [
                        BoxShadow(
                            color: isRecording ? Colors.white : Colors.black12,
                            spreadRadius: 4)
                      ], color: Colors.brown, shape: BoxShape.circle),
                      child: GestureDetector(
                        onLongPress: () {
                          _startRecord();
                          setState(() {
                            isRecording = true;
                          });
                        },
                        onLongPressEnd: (details) {
                          _stopRecord();
                          Future.delayed(const Duration(milliseconds: 3000),
                              () => _sendAudio());

                          setState(() {
                            isRecording = false;
                          });
                        },
                        child: Container(
                            padding: const EdgeInsets.all(10),
                            child: const Icon(
                              Icons.mic,
                              color: Colors.white,
                              size: 20,
                            )),
                      )),
                  Container(
                    height: 40,
                    margin: const EdgeInsets.fromLTRB(5, 5, 10, 5),
                    decoration: const BoxDecoration(
                        color: Colors.brown, shape: BoxShape.circle),
                    child: IconButton(
                      icon: const Icon(
                        Icons.send,
                        color: Colors.white,
                        size: 20,
                      ),
                      onPressed: () {
                        sendMsg();
                      },
                    ),
                  ),
                ],
              ),
            ),
          )
        ]));
  }

  // Chat components
  buildItem(message) {
    var day =
        DateTime.fromMillisecondsSinceEpoch(int.parse(message['timestamp']))
            .day
            .toString();
    var month =
        DateTime.fromMillisecondsSinceEpoch(int.parse(message['timestamp']))
            .month
            .toString();
    var year =
        DateTime.fromMillisecondsSinceEpoch(int.parse(message['timestamp']))
            .year
            .toString()
            .substring(2);
    var date = '$day-$month-$year';
    var hour =
        DateTime.fromMillisecondsSinceEpoch(int.parse(message['timestamp']))
            .hour;
    var min =
        DateTime.fromMillisecondsSinceEpoch(int.parse(message['timestamp']))
            .minute;
    var ampm = '';
    if (hour > 12) {
      hour = hour % 12;
      ampm = 'pm';
    } else if (hour == 12) {
      ampm = 'pm';
    } else if (hour == 0) {
      hour = 12;
      ampm = 'am';
    } else {
      ampm = 'am';
    }

    return Padding(
        padding: EdgeInsets.only(
            top: 8,
            left: ((message['senderId'] == "User") ? 80 : 10),
            right: ((message['senderId'] == "Bot") ? 10 : 80)),
        child: Container(
          width: MediaQuery.of(context).size.width * 0.5,
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: (message['senderId'] == "User") ? Colors.brown : Colors.grey,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Expanded(
                  child: Text(message['content'] + "\n",
                      textAlign: TextAlign.left))
              // Text(
              //   "$date $hour:$min$ampm",
              //   style: const TextStyle(fontSize: 10),
              // )
            ],
          ),
        ));
  }

  Future<bool> checkPermission() async {
    if (!await Permission.microphone.isGranted) {
      PermissionStatus status = await Permission.microphone.request();
      if (status != PermissionStatus.granted) {
        return false;
      }
    }
    return true;
  }

  // Text to speech
  void speak(String msg) {
    tts.setVolume(volume);
    tts.setRate(rate);
    tts.setLanguage("en-US");
    tts.setPitch(pitch);
    tts.speak(msg);
  }

  // Speech to text
  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

  void _startRecord() async {
    bool hasPermission = await checkPermission();
    print("Beginning");
    if (hasPermission) {
      await _speechToText.listen(onResult: _onSpeechResult);
    }
  }

  void _onSpeechResult(SpeechRecognitionResult result) {
    setState(() {
      _audioMsg = result.recognizedWords;
    });
  }

  void _stopRecord() async {
    await _speechToText.stop();
  }

  void _sendAudio() async {
    print(_audioMsg);
    _chatMessages.add({
      "senderId": "User",
      'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
      'content': _audioMsg,
      'type': 'text'
    });
    if (_audioMsg.isNotEmpty) {
      setState(() {
        isSending = true;
      });
    }
    String? chatRep = await retrieveApiResponse(_audioMsg);
    print(chatRep);
    if (chatRep != null) {
      _chatMessages.add({
        "senderId": "Bot",
        'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
        'content': chatRep,
        'type': 'text'
      });
      speak(chatRep);
    } else {
      _chatMessages.add({
        "senderId": "Bot",
        'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
        'content': "Sorry I didn't understand",
        'type': 'text'
      });
      speak("Sorry I didn't understand");
    }
  }

  // Chat
  sendMsg() async {
    setState(() {
      isSending = true;
    });

    _textMsg = _tec.text.trim();

    if (_textMsg.isNotEmpty) {
      _chatMessages.add({
        "senderId": "User",
        'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
        'content': _textMsg,
        'type': 'text'
      });
      setState(() {
        _chatMessages = _chatMessages;
      });
      _tec.clear();
    }
    String? chatRep = await retrieveApiResponse(_textMsg);
    if (chatRep != null) {
      _chatMessages.add({
        "senderId": "Bot",
        'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
        'content': chatRep,
        'type': 'text'
      });
      speak(chatRep);
    } else {
      _chatMessages.add({
        "senderId": "Bot",
        'timestamp': DateTime.now().millisecondsSinceEpoch.toString(),
        'content': "Sorry I didn't understand",
        'type': 'text'
      });
      speak("Sorry I didn't understand");
    }
    setState(() {
      _chatMessages = _chatMessages;
    });
    isSending = false;
  }

  retrieveApiResponse(String message) async {
    print("uploading");
    String apiUrl = 'http://172.20.10.12:5002/webhooks/rest/webhook';
    var url = Uri.parse(apiUrl);
    var body = {'message': message};

    String? jsonResponse = null;

    var response = await http.post(url, body: json.encode(body));
    if (response.statusCode == 200) {
      jsonResponse = jsonDecode(response.body)[0]['text'];
    }

    return jsonResponse;
  }
}

class ObservableList<T> {
  final _list = <T>[];

  final _itemAddedStreamController = StreamController<T>.broadcast();

  final _listStreamController = StreamController<List<T>>.broadcast();

  Stream get itemAddedStream => _itemAddedStreamController.stream;

  Stream get listStream => _listStreamController.stream;

  void add(T value) {
    _list.add(value);
    _itemAddedStreamController.add(value);
    _listStreamController.add(_list.reversed.toList());
  }

  void dispose() {
    _listStreamController.close();
    _itemAddedStreamController.close();
  }
}
