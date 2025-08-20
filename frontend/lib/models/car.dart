class Car {
  final String name;
  final String brand;
  final String model;
  final int year;
  final int price;
  final int mileage;
  final String transmission;
  final String fuel;
  final int power;
  final String datePosted;

  Car({
    required this.name,
    required this.brand,
    required this.model,
    required this.year,
    required this.price,
    required this.mileage,
    required this.transmission,
    required this.fuel,
    required this.power,
    required this.datePosted,
  });

  factory Car.fromMap(Map<String, dynamic> map) {
    return Car(
      name: map["name"] ?? "",
      brand: map["brand"] ?? "",
      model: map["model"] ?? "",
      year: map["year"] ?? 0,
      price: map["price"] ?? 0,
      mileage: map["mileage"] ?? 0,
      transmission: map["transmission"] ?? "",
      fuel: map["fuel"] ?? "",
      power: map["power"] ?? 0,
      datePosted: map["date_posted"] ?? "",
    );
  }
}
