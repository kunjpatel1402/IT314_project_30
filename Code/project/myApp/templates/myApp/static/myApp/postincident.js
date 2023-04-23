

function showOptions() {
  // Get the value of the selected radio button
  var crimeOrHazard = document.querySelector('input[name="crime-or-hazard"]:checked').value;

  // Get the dropdown element
  var dropdown = document.getElementById("dropdown");

  // Clear previous options
  dropdown.innerHTML = "";

  // Add new options based on the selected radio button
  if (crimeOrHazard === "crime") {
    var options = ["Murder", "Rape", "Kidnap", "Hit and Run", "Bribe", "CyberCrime", "Smuggling", "Theft", "Money Laundering", "Tax Fraud"];
  } else if (crimeOrHazard === "hazard") {
    var options = ["Fire", "Flood", "Earthquake", "Landslide", "Virus and Bacteria", "Tsunami", "Cyclone", "Drought", "Forest Fire", "Industrial Accident"];
  }

  // Add the options to the dropdown
  for (var i = 0; i < options.length; i++) {
    var option = document.createElement("option");
    option.text = options[i];
    dropdown.add(option);
  }
}