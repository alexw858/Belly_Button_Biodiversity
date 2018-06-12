var $selector = document.getElementById("selDataset")


function getOptions() {
    Plotly.d3.json('/names', function(error, sampleNames) {
        for (var i=0; i<sampleNames.length; i++) {
            var currentOption = document.createElement('option');
            currentOption.text === sampleNames[i];
            currentOption.value === sampleNames[i];
            $selector.appendChild(currentOption);
            // console.log(sampleNames[i]);
            // console.log(currentOption.text);
            // console.log(currentOption.value);
            console.log(currentOption);
        }
    // console.log(sampleNames);
    // console.log(currentOption);
    }
)}
getOptions()

// function optionChanged(dataset) {

// }