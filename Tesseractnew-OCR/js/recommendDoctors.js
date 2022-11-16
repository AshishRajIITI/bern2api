async function recommendDoctors() {
    //const diseaseNames = document.getElementById("results").value;
    
    //TODO: change below
    const diseaseNames=["vigbo", "fvdvf", "vigbo", "fvdvf", "vigbo", "fvdvf", "vigbo", "fvdvf"]
    // const numberOfDiseaseNames = diseaseNames.length;
    const numberOfDiseaseNames = 6;
    // console.log(diseaseNames);
    const doctorRecommendationList = [];

    for(let i=0;i<numberOfDiseaseNames; i++){

      const response = await fetch('http://localhost:5000/text-search',{ method: 'POST',
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