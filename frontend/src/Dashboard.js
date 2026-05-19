import React from "react";

import "./Dashboard.css";

function Dashboard() {

  const riskStudents = 18;
  const safeStudents = 102;
  const counselling = 12;
  const interventions = 27;

  return (

    <div className="dashboard">

      <h2>Faculty & HOD Dashboard</h2>

      <div className="cards">

        <div className="card">
          <h3>Total Students</h3>
          <p>120</p>
        </div>

        <div className="card">
          <h3>At Risk Students</h3>
          <p>{riskStudents}</p>
        </div>

        <div className="card">
          <h3>Counselling Referrals</h3>
          <p>{counselling}</p>
        </div>

        <div className="card">
          <h3>Interventions Applied</h3>
          <p>{interventions}</p>
        </div>

      </div>

      <div className="trend-section">

        <h3>Semester Risk Trends</h3>

        <table>

          <thead>

            <tr>
              <th>Month</th>
              <th>Risk Students</th>
              <th>Improvement %</th>
            </tr>

          </thead>

          <tbody>

            <tr>
              <td>January</td>
              <td>28</td>
              <td>12%</td>
            </tr>

            <tr>
              <td>February</td>
              <td>22</td>
              <td>21%</td>
            </tr>

            <tr>
              <td>March</td>
              <td>18</td>
              <td>35%</td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default Dashboard;