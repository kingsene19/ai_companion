import "package:flutter/material.dart";
import "package:font_awesome_flutter/font_awesome_flutter.dart";
import 'upload_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _classe = "";
  String _field = "";
  final TextEditingController _classeFieldController = TextEditingController();
  final TextEditingController _fieldFieldController = TextEditingController();

  _displayDialog(BuildContext context) async {
    return showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text('Specify the class'),
            content:
                Column(mainAxisAlignment: MainAxisAlignment.center, children: [
              TextField(
                controller: _classeFieldController,
                decoration: const InputDecoration(hintText: "Enter class"),
              ),
              TextField(
                controller: _fieldFieldController,
                decoration: const InputDecoration(hintText: "Enter field"),
              ),
            ]),
            actions: [
              TextButton(
                child: const Text('SUBMIT'),
                onPressed: () {
                  setState(() {
                    _classe = _classeFieldController.text;
                    _field = _fieldFieldController.text;
                  });
                  Navigator.of(context).pop();
                },
              )
            ],
          );
        });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Image(
                image: AssetImage('logo.png'),
                width: 300,
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: SizedBox(
                  height: 60,
                  width: 300,
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      await _displayDialog(context);
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => UploadPage(
                              fileType: "schedule",
                              classe: _classe,
                              field: _field)));
                    },
                    icon: const Icon(
                      FontAwesomeIcons.calendar,
                      size: 40,
                    ),
                    label: const Padding(
                        padding: EdgeInsets.symmetric(),
                        child: Text(
                          "Upload the schedule",
                          style: TextStyle(),
                        )),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.brown,
                      side: const BorderSide(width: 1, color: Colors.brown),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: SizedBox(
                  height: 60,
                  width: 300,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) =>
                              const UploadPage(fileType: "menu")));
                    },
                    icon: const Icon(
                      FontAwesomeIcons.list,
                      size: 40,
                    ),
                    label: const Padding(
                        padding: EdgeInsets.symmetric(),
                        child: Text(
                          "Upload the menu",
                          style: TextStyle(),
                        )),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.brown,
                      side: const BorderSide(width: 1, color: Colors.brown),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
