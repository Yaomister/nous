import { Formik } from "formik";
import toast, { Toaster } from "react-hot-toast";

import "../stylesheets/LoginForm.css";
import { api } from "../axios";
import { useNavigate } from "react-router-dom";
import { useTokenStore } from "../token.js";
import { useAuth } from "./AuthContext.jsx";

export const LoginForm = () => {
  const setToken = useTokenStore.getState().setToken;
  const { login } = useAuth();

  const navigate = useNavigate();
  return (
    <div className="login-form-wrapper">
      <Toaster></Toaster>

      <Formik
        initialValues={{
          email: "",
          password: "",
        }}
        onSubmit={async (values) => {
          try {
            const { status, data } = await api.post("/user/login", values, {
              withCredentials: true,
            });

            if (status === 200) {
              setToken(data.token);
              login();
              toast.success("Successfully logged in!", {
                onClose: () => navigate("/"),
              });
            }
          } catch (e) {
            toast.error("Log in failed");
            console.error(e);
          }
        }}
      >
        {(formik) => (
          <form
            className="dark-themed-form login-form"
            onSubmit={formik.handleSubmit}
          >
            <div className="login-form-title-wrapper">
              <h4 className="login-form-title">Welcome back</h4>
              <p className="login-form-subtitle">Good to see you again!</p>
            </div>

            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                type="text"
                id="email"
                name="email"
                placeholder="your.email@address.com"
                value={formik.values.email}
                onChange={formik.handleChange}
              />
            </div>
            <div className="field">
              <div className="login-password-label-wrapper">
                <label htmlFor="password">Password</label>
                <a href="/recover">Forgot password?</a>
              </div>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="password"
                value={formik.values.password}
                onChange={formik.handleChange}
              />
            </div>
            <div className="form-buttons-wrapper">
              <button type="submit" className="form-submit-button">
                Sign in
              </button>
              <a href="/register">Or sign up</a>
            </div>
          </form>
        )}
      </Formik>
    </div>
  );
};
