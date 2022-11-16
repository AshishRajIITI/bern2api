function getResults() {
    const result = [];
    const textareavalue = document.getElementById("log").value;
  
    const res = fetch('http://localhost:3003/bern2',{ method: 'POST',
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
      // console.log('Success: ', data);
      const annotations = data['annotations']
      annotations.forEach((a)=>{
        if(a["obj"]==="disease"){
          result.push(a["mention"])
        }
      })
    document.getElementById("results").innerHTML = result.join('<br/> ');
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    document.getElementById("results").value = result;

  }