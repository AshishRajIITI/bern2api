function getSummarizedReport() {
    const textareavalue = document.getElementById("log").value;
  
    const res = fetch('http://localhost:5000/summarizer',{ method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
     body: JSON.stringify({
      "text":textareavalue
    })})
    .then((response) => {
      return response.json();
      // console.log("raw response", response)
    })
    .then((data) => {
      //TODO: CHECK HERE
        // console.log("data", data)
      const result = data     
      document.getElementById("summarizer").innerHTML = result;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }