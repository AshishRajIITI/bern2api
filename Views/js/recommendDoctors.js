function arrToUl(root, arr) {
  var ul = document.createElement('ul');
  var li;
  document.getElementById("recommendationSpinner").classList.remove('spinner-border'); 
  root.appendChild(ul); // append the created ul to the root

  arr.forEach(function(item) {
    
    li = document.createElement('li'); // create a new list item
    card=document.createElement('div')
    card.appendChild(document.createElement('span').appendChild(document.createTextNode(item.name)))
    card.appendChild(document.createElement('br'))
    

    card.appendChild(document.createElement('span').appendChild(document.createTextNode(item.clinic)))
    card.appendChild(document.createElement('span').appendChild(document.createTextNode(", ")))
    var span_ = document.createElement('span')
    span_.innerHTML = item.address;
    span_.style.textDecoration = "none";
    
    card.appendChild(span_);

    card.appendChild(document.createElement('br'))
    


    li.appendChild(card); // append the text to the li
    ul.appendChild(li); // append the list item to the ul
  });
}

async function callDoctorApi(disease){
  try {
    const response= await fetch('http://localhost:5000/doctors',{ method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({      
      "disease": disease
    })})
    const data= await response.json()
    doctors_list = data.output;

      // document.getElementById("recommendations").innerHTML = doctorRecommendationList.join('<br/> ');
    return doctors_list;
  } catch (error) {
    console.error('Error:', error);
  }
  return [];
}


async function recommendDoctors() {
    document.getElementById("recommendationSpinner").classList.add('spinner-border'); 
    const diseaseNames = document.getElementById("results").value;    
    const numberOfDiseaseNames = diseaseNames.length;
    const promise=[]
    for(let i=0;i<numberOfDiseaseNames; i++){
      promise.push(callDoctorApi(diseaseNames[i]))
    }
    let doctors_list = await Promise.all(promise)
    let doctors_list_final = []
    
   

    for(let i=0; i<doctors_list.length;i++){
      for(let j=0; j<doctors_list[i].length;j++){
        let present_doc = doctors_list[i][j];
        if(!doctors_list_final.find((doctor) => present_doc.name===doctor.name))
         doctors_list_final.push(present_doc);
      }
    }
    // console.log("doctpr",doctors_list_final)

    
    arrToUl(document.getElementById("recommendations"), doctors_list_final);
  }