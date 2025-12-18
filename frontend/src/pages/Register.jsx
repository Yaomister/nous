import { RegisterForm } from "../components/RegisterForm";

import "../stylesheets/Register.css";

export const Register = () => {
  return (
    <div className="register-page-wrapper">
      <div className="register-page-left"></div>
      <div className="register-page-right">
        <RegisterForm />
      </div>
    </div>
  );
};
