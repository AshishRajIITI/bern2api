function getSummarizedReport() {
    const textareavalue = document.getElementById("log").value;
  
    const res = fetch('http://localhost:5000/summarizer',{ method: 'POST',
    headers: {
       'Content-Type': 'application/json',
    },
     body: JSON.stringify({
      //TODO:change it
      // "text":textareavalue
      "text": `FINAL REPORT i      PORTABLE AP CHEST FILM __ AT ___
      CLINICAL INDICATION: __ -year-old with nasogastric tube placement.
      Comparison to prior study dated ___ at ___.
      A series of three portable AP sequential images of the chest, the first at
      ___, the second at __ and the third at ___, are submitted.
      IMPRESSION:
      There has been interval attempted placement of a nasogastric tube which
      courses into the stomach but the tip ends up in the mid esophagus on all three
      images. Overall, cardiac and mediastinal contours are stable. Lungs are
      relatively well inflated. The subtle opacity in the right mid lung on the
      previous study does not persist and therefore is felt to correspond to an area
      of patchy atelectasis. No focal airspace consolidation is seen to suggest
      pneumonia. No pleural effusions or pneumothorax.`
    })})
    .then((response) => {  
      const x = response;    
      console.log("raw response", x)
      return x;
    })
    .then((data) => {
      //TODO: CHECK HERE
      console.log("data", data)
      const result = data     
      document.getElementById("summarizer").innerHTML = result;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }