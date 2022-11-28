async function getSummarizedReport() {
    document.getElementById("summarizerSpinner").classList.add('spinner-border'); 
    const textareavalue = document.getElementById("log").value;
  
    const response = await fetch('http://localhost:5000/summarizer',{ method: 'POST',
    headers: {
       'Content-Type': 'application/json',
    },
     body: JSON.stringify({      
      "text":textareavalue
    })});


    const result = await response.json() 
    // console.log("Re", result);   
    document.getElementById("summarizerSpinner").classList.remove('spinner-border'); 
    document.getElementById("summarizer").innerHTML = result["output"];
   
  }