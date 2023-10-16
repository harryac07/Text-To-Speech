import React from "react";

const FileUpload = ({ onUpload }) => {
  const handleChange = (event) => {
    onUpload(event.target.files[0]);
  };

  return (
    <input onChange={handleChange} accept={true} id="file-upload" type="file" />
  );
};

export default FileUpload;
