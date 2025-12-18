import { LoginForm } from "../components/LoginForm";
import "../stylesheets/Login.css";

export const Login = () => {
  return (
    <div className="login-page-wrapper">
      <div className="register-page-left"></div>
      <div className="register-page-right">
        <LoginForm />
      </div>
    </div>
  );
};
