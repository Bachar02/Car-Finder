import 'package:flutter/material.dart';
import 'screens/car_search_page.dart';

void main() {
  runApp(CarApp());
}

class CarApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Car Finder',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: CarSearchPage(),
    );
  }
}
