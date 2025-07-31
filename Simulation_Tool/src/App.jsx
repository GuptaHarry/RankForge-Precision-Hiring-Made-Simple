// import React, { useState } from "react";

// // Generate 300 dummy users
// const generateDummyUsers = () => {
//   return Array.from({ length: 300 }, (_, i) => ({
//     id: i + 1,
//     name: `User${i + 1}`,
//     roc: Math.floor(Math.random() * 100),
//     gpr: Math.floor(Math.random() * 100),
//     grd: Math.floor(Math.random() * 100),
//   }));
// };


// const RankForge = () => {
//   const [users] = useState(generateDummyUsers());
//   const [role, setRole] = useState("all");
//   const [topN, setTopN] = useState("all");
  
//   // User-defined thresholds for each role
//   const [thresholds, setThresholds] = useState({
//     sde: { roc: 70, gpr: 30, grd: 60 },
//     frontend: { roc: 50, gpr: 35, grd: 70 },
//     backend: { roc: 50, gpr: 35, grd: 70 }
//   });

//   // Handle threshold changes
//   const handleThresholdChange = (role, field, value) => {
//     setThresholds(prev => ({
//       ...prev,
//       [role]: { ...prev[role], [field]: parseInt(value) || 0 }
//     }));
//   };

//   // Filter and sort users
//   const getFilteredUsers = () => {
//     if (role === "all") return [...users];
    
//     const { roc, gpr, grd } = thresholds[role];
//     return users.filter(user => 
//       user.roc >= roc && 
//       user.gpr >= gpr && 
//       user.grd >= grd
//     );
//   };

//   const filteredUsers = getFilteredUsers();
//   const sortedUsers = [...filteredUsers].sort((a, b) => 
//     (b.roc + b.gpr + b.grd) - (a.roc + a.gpr + a.grd)
//   );
  
//   const displayedUsers = topN === "all" 
//     ? sortedUsers 
//     : sortedUsers.slice(0, parseInt(topN));

//   return (
//     <div style={{
//       fontFamily: 'Arial, sans-serif',
//       backgroundColor: 'white',
//       padding: '20px',
//       color: 'black',
//       width: '100vw',
//       margin: 0,
//       boxSizing: 'border-box',
//       overflowX: 'auto'
//     }}>
//       <h1 style={{ color: 'black', marginLeft: '20px' }}>RankForge Candidate Filter</h1>
      
//       {/* Role Selection */}
//       <div style={{ margin: '20px', display: 'flex', alignItems: 'center' }}>
//         <label style={{ marginRight: '10px' }}>Select Role:</label>
//         <select 
//           value={role} 
//           onChange={(e) => setRole(e.target.value)}
//           style={{ padding: '8px', minWidth: '150px' }}
//         >
//           <option value="all">All Users</option>
//           <option value="sde">SDE</option>
//           <option value="frontend">Frontend</option>
//           <option value="backend">Backend</option>
//         </select>
//       </div>

//       {/* Threshold Inputs */}
//       {role !== "all" && (
//         <div style={{ 
//           margin: '20px',
//           padding: '15px',
//           border: '1px solid #ddd',
//           borderRadius: '5px'
//         }}>
//           <h3>Set Minimum Thresholds for {role.toUpperCase()}:</h3>
//           <div style={{ display: 'flex', gap: '15px', marginTop: '10px', flexWrap: 'wrap' }}>
//             {['roc', 'gpr', 'grd'].map((field) => (
//               <div key={field} style={{ display: 'flex', alignItems: 'center' }}>
//                 <label style={{ marginRight: '5px', minWidth: '40px' }}>{field.toUpperCase()}:</label>
//                 <input
//                   type="number"
//                   value={thresholds[role][field]}
//                   onChange={(e) => handleThresholdChange(role, field, e.target.value)}
//                   style={{ padding: '8px', width: '80px' }}
//                 />
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Display Options */}
//       <div style={{ margin: '20px', display: 'flex', alignItems: 'center' }}>
//         <label style={{ marginRight: '10px' }}>Show:</label>
//         <select 
//           value={topN} 
//           onChange={(e) => setTopN(e.target.value)}
//           style={{ padding: '8px', minWidth: '150px' }}
//         >
//           <option value="all">All Candidates</option>
//           <option value="50">Top 50</option>
//           <option value="100">Top 100</option>
//           <option value="150">Top 150</option>
//         </select>
//       </div>

//       {/* Results */}
//       <div style={{ margin: '20px' }}>
//         <h3>
//           Showing {displayedUsers.length} {role !== "all" ? "qualified" : ""} candidates
//           {role !== "all" && ` (from ${filteredUsers.length} who meet thresholds)`}
//         </h3>
        
//         <div style={{ overflowX: 'auto', width: '100%' }}>
//           <table style={{ 
//             width: '100%', 
//             borderCollapse: 'collapse',
//             marginTop: '15px',
//             tableLayout: 'auto',
//             minWidth: '800px'
//           }}>
//             <thead>
//               <tr style={{ 
//                 backgroundColor: '#f2f2f2',
//                 borderBottom: '1px solid #ddd'
//               }}>
//                 <th style={{ padding: '12px', textAlign: 'left', minWidth: '80px' }}>Rank</th>
//                 <th style={{ padding: '12px', textAlign: 'left', minWidth: '120px' }}>Name</th>
//                 <th style={{ padding: '12px', textAlign: 'center', minWidth: '100px' }}>ROC</th>
//                 <th style={{ padding: '12px', textAlign: 'center', minWidth: '100px' }}>GPR</th>
//                 <th style={{ padding: '12px', textAlign: 'center', minWidth: '100px' }}>GRD</th>
//                 <th style={{ padding: '12px', textAlign: 'center', minWidth: '100px' }}>Total</th>
//               </tr>
//             </thead>
//             <tbody>
//               {displayedUsers.map((user, index) => (
//                 <tr 
//                   key={user.id}
//                   style={{ 
//                     borderBottom: '1px solid #ddd',
//                     ':hover': { backgroundColor: '#f9f9f9' }
//                   }}
//                 >
//                   <td style={{ padding: '12px' }}>{index + 1}</td>
//                   <td style={{ padding: '12px' }}>{user.name}</td>
//                   <td style={{ 
//                     padding: '12px', 
//                     textAlign: 'center',
//                     color: role !== "all" && user.roc < thresholds[role].roc ? 'red' : 'black',
//                     fontWeight: role !== "all" && user.roc < thresholds[role].roc ? 'normal' : 'bold'
//                   }}>
//                     {user.roc}
//                   </td>
//                   <td style={{ 
//                     padding: '12px', 
//                     textAlign: 'center',
//                     color: role !== "all" && user.gpr < thresholds[role].gpr ? 'red' : 'black',
//                     fontWeight: role !== "all" && user.gpr < thresholds[role].gpr ? 'normal' : 'bold'
//                   }}>
//                     {user.gpr}
//                   </td>
//                   <td style={{ 
//                     padding: '12px', 
//                     textAlign: 'center',
//                     color: role !== "all" && user.grd < thresholds[role].grd ? 'red' : 'black',
//                     fontWeight: role !== "all" && user.grd < thresholds[role].grd ? 'normal' : 'bold'
//                   }}>
//                     {user.grd}
//                   </td>
//                   <td style={{ 
//                     padding: '12px', 
//                     textAlign: 'center',
//                     fontWeight: 'bold'
//                   }}>
//                     {user.roc + user.gpr + user.grd}
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default RankForge;
import React from "react";
import  { useState } from "react";


const generateDummyUsers = () => {
  const roles = ["sde", "frontend", "backend"];
  return Array.from({ length: 300 }, (_, i) => {
    const role = roles[Math.floor(Math.random() * roles.length)];
    const rocBase = role === "sde" ? 60 : Math.random() * 40;
    const gprBase = role === "frontend" ? 60 : Math.random() * 40;
    const grdBase = role === "backend" ? 60 : Math.random() * 40;

    return {
      id: i + 1,
      name: `User${i + 1}`,
      roc: Math.min(100, Math.floor(rocBase + Math.random() * 40)),
      gpr: Math.min(100, Math.floor(gprBase + Math.random() * 40)),
      grd: Math.min(100, Math.floor(grdBase + Math.random() * 40)),
    };
  });
};

const RankForge = () => {
  const [users] = useState(generateDummyUsers());
  const [role, setRole] = useState("all");
  const [topN, setTopN] = useState("all");
  const [sorted, setSorted] = useState(false);
  const [highlightedIds, setHighlightedIds] = useState([]);

  const [thresholds, setThresholds] = useState({
    sde: { roc: 70, gpr: 30, grd: 60 },
    frontend: { roc: 50, gpr: 35, grd: 70 },
    backend: { roc: 50, gpr: 35, grd: 70 },
  });

  const handleThresholdChange = (role, field, value) => {
    const parsedValue = value === "" ? "" : parseInt(value) || 0;
    setThresholds((prev) => ({
      ...prev,
      [role]: { ...prev[role], [field]: parsedValue },
    }));
    setSorted(false);
  };

  const getFilteredUsers = () => {
    if (role === "all") return [...users];
    const { roc, gpr, grd } = thresholds[role];
    return users.filter(
      (user) =>
        user.roc >= (roc || 0) &&
        user.gpr >= (gpr || 0) &&
        user.grd >= (grd || 0)
    );
  };

  const filteredUsers = getFilteredUsers();
  const sortedUsers = sorted
    ? [...filteredUsers].sort(
        (a, b) => b.roc + b.gpr + b.grd - (a.roc + a.gpr + a.grd)
      )
    : filteredUsers;

  const displayedUsers =
    topN === "all" ? sortedUsers : sortedUsers.slice(0, parseInt(topN));

  const handleSort = () => {
    const ids = filteredUsers
      .sort((a, b) => b.roc + b.gpr + b.grd - (a.roc + a.gpr + a.grd))
      .map((u) => u.id);
    setHighlightedIds(ids);
    setSorted(true);
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }, 50);
  };

  const resetSorting = () => {
    setSorted(false);
    setHighlightedIds([]);
  };

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        backgroundColor: "white",
        padding: "20px",
        color: "black",
        width: "100vw",
        boxSizing: "border-box",
        overflowX: "auto",
      }}
    >
      <h1 style={{ color: "#333", marginLeft: "20px" }}>
        RankForge Candidate Filter
      </h1>

      {/* Role Selection */}
      <div style={{ margin: "20px", display: "flex", alignItems: "center" }}>
        <label style={{ marginRight: "10px" }}>Select Role:</label>
        <select
          value={role}
          onChange={(e) => {
            setRole(e.target.value);
            setSorted(false);
            setHighlightedIds([]);
          }}
          style={{ padding: "8px", minWidth: "150px" }}
        >
          <option value="all">All Users</option>
          <option value="sde">SDE</option>
          <option value="frontend">Frontend</option>
          <option value="backend">Backend</option>
        </select>
      </div>

      {/* Threshold Inputs */}
      {role !== "all" && (
        <div
          style={{
            margin: "20px",
            padding: "15px",
            border: "1px solid #ddd",
            borderRadius: "5px",
          }}
        >
          <h3>Set Minimum Thresholds for {role.toUpperCase()}:</h3>
          <div
            style={{
              display: "flex",
              gap: "15px",
              marginTop: "10px",
              flexWrap: "wrap",
            }}
          >
            {["roc", "gpr", "grd"].map((field) => (
              <div key={field} style={{ display: "flex", alignItems: "center" }}>
                <label style={{ marginRight: "5px", minWidth: "40px" }}>
                  {field.toUpperCase()}:
                </label>
                <input
                  type="number"
                  value={
                    thresholds[role][field] === "" ? "" : thresholds[role][field]
                  }
                  onChange={(e) =>
                    handleThresholdChange(role, field, e.target.value)
                  }
                  style={{ padding: "8px", width: "80px" }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Display Options */}
      <div style={{ margin: "20px", display: "flex", alignItems: "center" }}>
        <label style={{ marginRight: "10px" }}>Show:</label>
        <select
          value={topN}
          onChange={(e) => setTopN(e.target.value)}
          style={{ padding: "8px", minWidth: "150px" }}
        >
          <option value="all">All Candidates</option>
          <option value="50">Top 50</option>
          <option value="100">Top 100</option>
          <option value="150">Top 150</option>
        </select>

        <button
          onClick={handleSort}
          style={{
            marginLeft: "20px",
            padding: "8px 15px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Sort Candidates
        </button>

        {sorted && (
          <button
            onClick={resetSorting}
            style={{
              marginLeft: "10px",
              padding: "8px 15px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Reset Sorting
          </button>
        )}
      </div>

      {/* Results */}
      <div style={{ margin: "20px" }}>
        <h3>
          Showing {displayedUsers.length}{" "}
          {role !== "all" ? "qualified" : ""} candidates
          {role !== "all" && ` (from ${filteredUsers.length} who meet thresholds)`}
        </h3>

        <div style={{ overflowX: "auto", width: "100%" }}>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              marginTop: "15px",
              tableLayout: "auto",
              minWidth: "800px",
            }}
          >
            <thead>
              <tr
                style={{
                  backgroundColor: "#f2f2f2",
                  borderBottom: "1px solid #ddd",
                }}
              >
                <th style={{ padding: "12px", textAlign: "left" }}>Rank</th>
                <th style={{ padding: "12px", textAlign: "left" }}>Name</th>
                <th style={{ padding: "12px", textAlign: "center" }}>ROC</th>
                <th style={{ padding: "12px", textAlign: "center" }}>GPR</th>
                <th style={{ padding: "12px", textAlign: "center" }}>GRD</th>
                <th style={{ padding: "12px", textAlign: "center" }}>Total</th>
              </tr>
            </thead>
            <tbody>
              {displayedUsers.map((user, index) => {
                const isHighlighted = highlightedIds.includes(user.id);
                return (
                  <tr
                    key={user.id}
                    style={{
                      borderBottom: "1px solid #ddd",
                      backgroundColor: isHighlighted ? "#e6f7ff" : "white",
                      transition: "background-color 0.3s ease",
                    }}
                  >
                    <td style={{ padding: "12px" }}>{index + 1}</td>
                    <td style={{ padding: "12px" }}>{user.name}</td>
                    <td
                      style={{
                        padding: "12px",
                        textAlign: "center",
                        color:
                          role !== "all" && user.roc < thresholds[role].roc
                            ? "red"
                            : "#0a8a0a",
                        fontWeight:
                          role !== "all" && user.roc < thresholds[role].roc
                            ? "normal"
                            : "bold",
                      }}
                    >
                      {user.roc}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        textAlign: "center",
                        color:
                          role !== "all" && user.gpr < thresholds[role].gpr
                            ? "red"
                            : "#0066cc",
                        fontWeight:
                          role !== "all" && user.gpr < thresholds[role].gpr
                            ? "normal"
                            : "bold",
                      }}
                    >
                      {user.gpr}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        textAlign: "center",
                        color:
                          role !== "all" && user.grd < thresholds[role].grd
                            ? "red"
                            : "#cc6600",
                        fontWeight:
                          role !== "all" && user.grd < thresholds[role].grd
                            ? "normal"
                            : "bold",
                      }}
                    >
                      {user.grd}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        textAlign: "center",
                        fontWeight: "bold",
                        color: "#444",
                      }}
                    >
                      {user.roc + user.gpr + user.grd}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default RankForge;
