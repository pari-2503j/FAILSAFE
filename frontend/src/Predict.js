import React, { useState } from "react";
import API from "./api";

import "./Predict.css";

function Predict() {

  const [result, setResult] = useState(null);

  const [form, setForm] = useState({

    school: "GP",
    sex: "F",
    age: 18,
    address: "U",
    famsize: "GT3",
    Pstatus: "A",
    Medu: 4,
    Fedu: 4,
    Mjob: "at_home",
    Fjob: "teacher",
    reason: "course",
    guardian: "mother",
    traveltime: 2,
    studytime: 1,
    failures: 2,
    schoolsup: "yes",
    famsup: "no",
    paid: "no",
    activities: "no",
    nursery: "yes",
    higher: "yes",
    internet: "no",
    romantic: "no",
    famrel: 4,
    freetime: 3,
    goout: 4,
    Dalc: 1,
    Walc: 1,
    health: 3,
    absences: 20

  });

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    });

  };

  const predictStudent = async () => {

    try {

      const token = localStorage.getItem("token");

      const response = await API.post(
        "/predict",
        form,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult(response.data);

    } catch (err) {

      console.log(err);

      alert("Prediction Failed");

    }
  };

  const generateIntervention = () => {

    if (!result) return [];

    let plans = [];

    if (form.absences > 10) {
      plans.push("Attendance counselling referral");
    }

    if (form.failures >= 2) {
      plans.push("Academic remediation classes");
    }

    if (form.studytime <= 1) {
      plans.push("Personalized study plan adjustment");
    }

    if (form.goout >= 4) {
      plans.push("Behavioural mentoring session");
    }

    return plans;
  };

  return (

    <div className="predict-container">

      <h2>Student Risk Analysis</h2>

      <div className="form-grid">

        {Object.keys(form).map((key) => (

          <input
            key={key}
            name={key}
            value={form[key]}
            onChange={handleChange}
            placeholder={key}
          />

        ))}

      </div>

      <button onClick={predictStudent}>
        Predict Risk
      </button>

      {result && (

        <div className="result-card">

          <h3>

            {result.risk_prediction === 1
              ? "AT RISK STUDENT"
              : "SAFE STUDENT"}

          </h3>

          <p>
            Risk Probability:
            {(result.risk_probability * 100).toFixed(2)}%
          </p>

          <h4>SHAP Risk Factors</h4>

          <ul>

            {Object.entries(result.shap_values).map(([key, value]) => (

              <li key={key}>
                {key} : {value.toFixed(3)}
              </li>

            ))}

          </ul>

          <h4>Auto Intervention Plan</h4>

          <ul>

            {generateIntervention().map((plan, index) => (

              <li key={index}>
                {plan}
              </li>

            ))}

          </ul>

        </div>

      )}

    </div>
  );
}

export default Predict;