// Importing express module
const express = require("express");
const app = express();
const axios = require("axios");
var cors = require('cors')
app.use(cors())

app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) 


app.post("/bern2", async (req, res) => {
  console.log("request",req.body)
  try {
    const result = await axios({
      method: "post",
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


// Server setup
app.listen(3003, () => {
  console.log("Server is Running");
});
