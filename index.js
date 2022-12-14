// Importing express module
const express = require("express");
const app = express();
const axios = require("axios");
var cors = require('cors')
const dotenv = require('dotenv');
dotenv.config();

app.use(cors())
app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) 


app.post("/bern2", async (req, res) => {
  console.log("request",req.body)
  try {
    const result = await axios({
      method: "post",
      //If you are using the model running on local environment, use below
      // url="http://localhost:8888/plain",

      //if(machine incompatible), use the already hosted model by the bern2 team
      url: "http://bern2.korea.ac.kr/plain",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      data: req.body,
    });
    // console.log(result);
    return res.status(200).json(result.data);
  } catch (error) {
    return res.status(400).json("An error occured");
  }
});


//TODO: google-maps-api endpont
const key = process.env.GOOGLE_API_KEY
app.post('/text-search', async (req, res) => {
 try {
   const disease  = req.body.disease;
   console.log(key);

   //TODO:remove below key=null line
   key = null;
   
   const {data} = await axios.get(   
  `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${disease}+Indore&type=doctor&key=${key}`
   )
   return res.json(data)
   } 
   catch (error) {
    console.log(error);
    return res.status(400).json("An error occured");
   }
})


// Server setup
app.listen(3003, () => {
  console.log("Server is Running");
});
