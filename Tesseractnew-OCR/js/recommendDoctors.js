async function recommendDoctors() {
    
    const doctorRecommendationList = [];    

    const diseaseNames = document.getElementById("results").value;    
    const numberOfDiseaseNames = diseaseNames.length;
    
    for(let i=0;i<numberOfDiseaseNames; i++){

      const response = await fetch('http://localhost:3003/text-search',{ method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({      
        "disease": diseaseNames[i]
      })})
      .then((response)=>{
        return response.json();
      })
      .then((data)=>{
        console.log(data);
        doctorRecommendationList.push(data);
        document.getElementById("recommendations").innerHTML = doctorRecommendationList.join('<br/> ');

      })
      .catch((error)=>{
        console.error('Error:', error);
      })

    }

    document.getElementById("recommendations").value = doctorRecommendationList;

  }