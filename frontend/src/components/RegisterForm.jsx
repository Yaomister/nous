import { Formik } from "formik";
import "../stylesheets/Forms.css";
import "../stylesheets/RegisterForm.css";
import { verifyRegister } from "../helpers/UserManagementHelpers";
import toast, { Toaster } from "react-hot-toast";
import { api } from "../axios";
import { useNavigate } from "react-router-dom";

export const RegisterForm = () => {
  const navigate = useNavigate();
  return (
    <div className="register-form-wrapper">
      <Toaster></Toaster>
      <Formik
        initialValues={{ username: "", password: "", email: "" }}
        onSubmit={async (values) => {
          const errors = verifyRegister({ ...values });

          if (errors.length > 0) {
            return toast.error(errors[0]);
          }

          try {
            console.error(api.getUri());
            const { status } = await api.post("/user/register", values);
            if (status == 201) {
              toast.success("Successfully registered!", {
                onClose: () => navigate("/login"),
              });
            }
          } catch (e) {
            console.error(e);
            toast.error("Could not register!");
          }
        }}
      >
        {(formik) => {
          return (
            <form
              onSubmit={formik.handleSubmit}
              className="dark-themed-form register-form"
            >
              <h4 className="register-form-title">Join our community</h4>
              <div className="field">
                <label htmlFor="email">Email address</label>
                <input
                  type="text"
                  required="true"
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  name="email"
                  placeholder="your.email@address.com"
                  id="email"
                />
              </div>
              <div className="field">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  required="true"
                  value={formik.values.username}
                  onChange={formik.handleChange}
                  name="username"
                  id="username"
                  placeholder="johndoe"
                />
              </div>
              <div className="field">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  required="true"
                  value={formik.values.password}
                  onChange={formik.handleChange}
                  name="password"
                  id="password"
                  placeholder="Choose your password"
                />
              </div>
              <p className="register-terms-and-services-text">
                By signing up you agree to our <a href="/">Privacy Policy</a>{" "}
                and <a href="/">Terms of Service</a>.
              </p>
              <div className="register-form-buttons-wrapper">
                <button type="submit" className="register-form-submit-button">
                  Sign up
                </button>
                <a href="/login">Or sign in</a>
              </div>
            </form>
          );
        }}
      </Formik>
    </div>
  );
};
