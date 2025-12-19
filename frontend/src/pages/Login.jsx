import { LoginForm } from "../components/LoginForm";
import "../stylesheets/FormPage.css";

export const Login = () => {
  return (
    <div className="form-page-wrapper">
      <div className="form-page-left"></div>
      <div className="form-page-right">
        <LoginForm />
      </div>
    </div>
  );
};
