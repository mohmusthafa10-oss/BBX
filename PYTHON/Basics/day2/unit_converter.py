try:
    celcius = float(input("Enter temperature in Celsius: "))
    
    fahrenheit = (celcius * 9/5) + 32
    
    print(f"Fahrenheit of {celcius}° Celsius is {fahrenheit:.1f}°")
    
except ValueError:
    print("Please enter a valid number.")