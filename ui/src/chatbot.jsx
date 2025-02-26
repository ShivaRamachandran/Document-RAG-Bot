
// import React, { useState } from "react";

// const ChatBot = () => {
//   const [query, setQuery] = useState("");
//   const [response, setResponse] = useState("");
//   const [conversation, setConversation] = useState([]);

//   const handleSend = async () => {
//     if (!query.trim()) return;

//     try {
//       const res = await fetch(`http://localhost:9898/query?question=${query}`);
//       const data = await res.json();
//       const newMessage = { user: query, bot: data.response };

//       setConversation([...conversation, newMessage]);
//       setQuery(""); // Clear input field
//     } catch (error) {
//       console.error("Error fetching response:", error);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen bg-orange-500 items-center justify-center p-6 relative">
//       {/* Top-right button for managing RAG documents */}
//       <button
//         className="absolute top-6 right-6 bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-900"
//         onClick={() => alert("Add/Delete RAG Documents")}
//       >
//         Manage RAG Docs
//       </button>

//       {/* Title */}
//       <h1 className="text-4xl font-bold mb-4 text-gray-800">RAG CHAT-BOT</h1>

//       {/* Chat Container */}
//       <div className="w-full max-w-2xl bg-white shadow-lg rounded-lg p-4 flex flex-col space-y-2 h-[500px] overflow-y-auto">
//         {conversation.map((msg, index) => (
//           <div key={index} className="flex flex-col space-y-2">
//             <p className="self-end bg-blue-500 text-white p-2 rounded-lg max-w-xs">
//               {msg.user}
//             </p>
//             <p className="self-start bg-gray-200 p-2 rounded-lg max-w-xs">
//               {msg.bot}
//             </p>
//           </div>
//         ))}
//       </div>

//       {/* Input Box */}
//       <div className="mt-4 flex w-full max-w-2xl">
//         <input
//           type="text"
//           className="flex-1 p-2 border border-gray-300 rounded-lg outline-none text-lg placeholder:text-lg"
//           placeholder="Input your query here..."
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//         />
//         <button
//           className="ml-2 bg-blue-500 text-white px-4 py-2 rounded-lg"
//           onClick={handleSend}
//         >
//           Send
//         </button>
//       </div>
//     </div>
//   );
// };

// export default ChatBot;

//  ==================================================================================================

import React, { useState, useEffect } from "react";

const ChatBot = () => {
  const [query, setQuery] = useState("");
  const [conversation, setConversation] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  const API_BASE = "http://localhost:9898"; // Update to match your FastAPI backend

  // Fetch list of documents
  const fetchDocuments = async () => {
    try {
      const res = await fetch(`${API_BASE}/list_docs`);
      const data = await res.json();
      setDocuments(data.documents);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  // Handle document upload
  const handleUpload = async () => {
    if (!selectedFile) return alert("Please select a file to upload!");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      alert(data.message);
      setSelectedFile(null);
      fetchDocuments();
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  // Handle document deletion
  const handleDelete = async (filename) => {
    try {
      const res = await fetch(`${API_BASE}/delete?filename=${filename}`, {
        method: "DELETE",
      });

      const data = await res.json();
      alert(data.message);
      fetchDocuments();
    } catch (error) {
      console.error("Delete failed:", error);
    }
  };

  // Handle user query
  const handleSend = async () => {
    if (!query.trim()) return;

    try {
      const res = await fetch(`${API_BASE}/query?question=${query}`);
      const data = await res.json();
      const newMessage = { user: query, bot: data.response };

      setConversation([...conversation, newMessage]);
      setQuery("");
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  // Open Modal
  const openModal = () => {
    fetchDocuments();
    setIsModalOpen(true);
  };

  return (
    <div className="flex flex-col h-screen bg-orange-500 items-center justify-center p-6 relative">
      {/* Top-right button for managing RAG documents */}
      <button
        className="absolute top-6 right-6 bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-900"
        onClick={openModal}
      >
        Manage RAG Docs
      </button>

      {/* Title */}
      <h1 className="text-4xl font-bold mb-4 text-gray-800">RAG CHAT-BOT</h1>

      {/* Chat Container */}
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-lg p-4 flex flex-col space-y-2 h-[500px] overflow-y-auto">
        {conversation.map((msg, index) => (
          <div key={index} className="flex flex-col space-y-2">
            <p className="self-end bg-blue-500 text-white p-2 rounded-lg max-w-xs">
              {msg.user}
            </p>
            <p className="self-start bg-gray-200 p-2 rounded-lg max-w-xs">
              {msg.bot}
            </p>
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="mt-4 flex w-full max-w-2xl">
        <input
          type="text"
          className="flex-1 p-2 border border-gray-300 rounded-lg outline-none text-lg placeholder:text-lg"
          placeholder="Input your query here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="ml-2 bg-blue-500 text-white px-4 py-2 rounded-lg"
          onClick={handleSend}
        >
          Send
        </button>
      </div>

      {/* Manage RAG Docs Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg w-96 shadow-lg">
            <h2 className="text-xl font-bold mb-4">Manage RAG Docs</h2>

            {/* File Upload */}
            <input
              type="file"
              className="mb-2 border p-2 w-full"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
            <button
              className="bg-green-500 text-white px-4 py-2 rounded-lg w-full mb-4"
              onClick={handleUpload}
            >
              Upload File
            </button>

            {/* List of Documents */}
            <h3 className="text-lg font-semibold mb-2">Available Documents</h3>
            <ul className="max-h-40 overflow-y-auto">
              {documents.length > 0 ? (
                documents.map((doc, index) => (
                  <li key={index} className="flex justify-between items-center border-b py-2">
                    <span>{doc}</span>
                    <button
                      className="bg-red-500 text-white px-2 py-1 rounded"
                      onClick={() => handleDelete(doc)}
                    >
                      Delete
                    </button>
                  </li>
                ))
              ) : (
                <p className="text-gray-500">No documents found</p>
              )}
            </ul>

            {/* Close Button */}
            <button
              className="mt-4 bg-gray-700 text-white px-4 py-2 rounded-lg w-full"
              onClick={() => setIsModalOpen(false)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBot;
