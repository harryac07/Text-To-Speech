import axios from "axios";
import { useState } from "react";
import FileUpload from "./Component/fileUpload";
import { Button, Select, MenuItem, Typography } from "@mui/material";

import "./App.css";
const speakAPI = "http://localhost:3002/speak";

const formData = new FormData();

const App = () => {
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [file, setFile] = useState();
  const [audioUrl, setAudioUrl] = useState("");

  const handleChange = (event) => {
    setSelectedLanguage(event.target.value);
    setAudioUrl("");
  };

  const handleFileUpload = (uploadedFile) => {
    setFile(uploadedFile);
    setAudioUrl("");
  };

  const handleSubmit = async () => {
    formData.append("file", file);
    // Handle upload
    try {
      const response = await axios.post(
        "http://localhost:3001/predict",
        formData
      );
      const number = response.data.number;

      const speakResponse = await axios.get(
        `${speakAPI}?number=${number}&language=${selectedLanguage}`,
        {
          responseType: "blob"
        }
      );
      // Create a Blob URL for the audio data
      const blob = new Blob([speakResponse.data], { type: "audio/mpeg" });
      const url = window.URL.createObjectURL(blob);

      // Set the audio URL
      setAudioUrl(url);
    } catch (e) {
      console.error("Error fetching audio:", e);
    }
  };

  return (
    <div className="app">
      <h2>Our App</h2>
      <div className="container">
        <div>
          <FileUpload onUpload={handleFileUpload} />
        </div>
        <div style={{ textAlign: "left" }}>
          <Typography>Select output language: </Typography>
          <Select
            value={selectedLanguage}
            label="Select Language"
            onChange={handleChange}
            size="small"
          >
            <MenuItem value={"en"}>English</MenuItem>
            <MenuItem value={"fi"}>Finnish</MenuItem>
            <MenuItem value={"sv"}>Swedish</MenuItem>
            <MenuItem value={"no"}>Norwegian</MenuItem>
            <MenuItem value={"fr"}>French</MenuItem>
          </Select>
        </div>
      </div>
      <Button size="small" variant="contained" onClick={handleSubmit}>
        Submit file
      </Button>

      {audioUrl && (
        <div style={{ margin: "32px 0px" }}>
          <hr />
          <h4>Play audio</h4>
          <audio controls src={audioUrl}></audio>
        </div>
      )}
    </div>
  );
};

export default App;
