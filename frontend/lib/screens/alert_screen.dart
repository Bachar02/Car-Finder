// frontend/lib/screens/alert_screen.dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AlertScreen extends StatefulWidget {
  @override
  _AlertScreenState createState() => _AlertScreenState();
}

class _AlertScreenState extends State<AlertScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _brandController = TextEditingController();
  final TextEditingController _maxPriceController = TextEditingController();
  final TextEditingController _maxMileageController = TextEditingController();
  final TextEditingController _minYearController = TextEditingController();
  String? _selectedFuelType;
  String? _selectedTransmission;

  final List<String> fuelTypes = ['Any', 'Petrol', 'Diesel', 'Electric', 'Hybrid'];
  final List<String> transmissions = ['Any', 'Automatic', 'Manual'];

  Future<void> _createAlert() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await http.post(
          Uri.parse('http://10.0.2.2:8000/api/alerts'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': 'current_user', // You can implement user auth later
            'brand': _brandController.text.isNotEmpty ? _brandController.text : null,
            'max_price': _maxPriceController.text.isNotEmpty ? int.parse(_maxPriceController.text) : null,
            'max_mileage': _maxMileageController.text.isNotEmpty ? int.parse(_maxMileageController.text) : null,
            'min_year': _minYearController.text.isNotEmpty ? int.parse(_minYearController.text) : null,
            'fuel_type': _selectedFuelType != 'Any' ? _selectedFuelType : null,
            'transmission': _selectedTransmission != 'Any' ? _selectedTransmission : null,
          }),
        );

        if (response.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Alert created successfully!'),
              backgroundColor: Colors.green,
            ),
          );
          _clearForm();
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to create alert'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _clearForm() {
    _brandController.clear();
    _maxPriceController.clear();
    _maxMileageController.clear();
    _minYearController.clear();
    _selectedFuelType = 'Any';
    _selectedTransmission = 'Any';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Car Alert'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              Text(
                'Get notified when matching cars are available',
                style: TextStyle(fontSize: 16, color: Colors.grey[600]),
              ),
              SizedBox(height: 20),

              TextFormField(
                controller: _brandController,
                decoration: InputDecoration(
                  labelText: 'Brand (optional)',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., BMW, Mercedes, Audi',
                ),
              ),
              SizedBox(height: 15),

              TextFormField(
                controller: _maxPriceController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Max Price € (optional)',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., 30000',
                ),
              ),
              SizedBox(height: 15),

              TextFormField(
                controller: _maxMileageController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Max Mileage km (optional)',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., 50000',
                ),
              ),
              SizedBox(height: 15),

              TextFormField(
                controller: _minYearController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Min Year (optional)',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., 2018',
                ),
              ),
              SizedBox(height: 15),

              DropdownButtonFormField<String>(
                value: _selectedFuelType ?? 'Any',
                decoration: InputDecoration(
                  labelText: 'Fuel Type',
                  border: OutlineInputBorder(),
                ),
                items: fuelTypes.map((type) => DropdownMenuItem(
                  value: type,
                  child: Text(type),
                )).toList(),
                onChanged: (value) => setState(() => _selectedFuelType = value),
              ),
              SizedBox(height: 15),

              DropdownButtonFormField<String>(
                value: _selectedTransmission ?? 'Any',
                decoration: InputDecoration(
                  labelText: 'Transmission',
                  border: OutlineInputBorder(),
                ),
                items: transmissions.map((type) => DropdownMenuItem(
                  value: type,
                  child: Text(type),
                )).toList(),
                onChanged: (value) => setState(() => _selectedTransmission = value),
              ),
              SizedBox(height: 25),

              ElevatedButton(
                onPressed: _createAlert,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  padding: EdgeInsets.symmetric(vertical: 16),
                ),
                child: Text('Create Alert', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}