import { Formik } from "formik";
import toast, { Toaster } from "react-hot-toast";

import "../stylesheets/Forms.css";
import "../stylesheets/RecoverForm.css";
import { useState } from "react";
import { api } from "../axios";

export const RecoverForm = () => {
  const [sentEmail, setSentEmail] = useState(false);
  return (
    <div className="recover-form-wrapper">
      <Toaster></Toaster>

      <Formik
        initialValues={{
          email: "",
        }}
        onSubmit={async (values) => {
          try {
            const { status } = await api.post(
              "/user/reset-password-link",
              values
            );

            if (status == 200) {
              setSentEmail(true);
            }
          } catch (e) {
            const status = e.response?.status;
            if (status === 422) {
              toast.error("Email not registered");
            } else {
              toast.error("Could not send reset link");
            }
          }
        }}
      >
        {(formik) => {
          return (
            <form
              className="dark-themed-form recover-form"
              onSubmit={formik.handleSubmit}
            >
              {sentEmail ? (
                <>
                  <div className="recover-form-title-wrapper">
                    <h4 className="form-title">Reset link sent!</h4>
                    <h4 className="form-subtitle">
                      Please check your email and follow the instructions
                    </h4>
                  </div>
                </>
              ) : (
                <>
                  <div className="recover-form-title-wrapper">
                    <h4 className="form-title">Forgotten your password?</h4>
                    <h4 className="form-subtitle">
                      We'll send you a reset link if your account exists
                    </h4>
                  </div>
                  <div className="field">
                    <label htmlFor="email">Email</label>
                    <input
                      required={true}
                      type="text"
                      id="email"
                      name="email"
                      placeholder="your.email@address.com"
                      value={formik.values.email}
                      onChange={formik.handleChange}
                    />
                  </div>
                  <div className="form-buttons-wrapper">
                    <button type="submit" className="form-submit-button">
                      Reset my password
                    </button>
                    <a href="/register">Or sign in</a>
                  </div>
                </>
              )}
            </form>
          );
        }}
      </Formik>
    </div>
  );
};
