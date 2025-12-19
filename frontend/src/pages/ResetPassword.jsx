import { Formik } from "formik";
import { useNavigate, useParams } from "react-router-dom";

import "../stylesheets/Forms.css";
import "../stylesheets/ResetPassword.css";
import { verifyResetPassword } from "../helpers/UserManagementHelpers";
import toast, { Toaster } from "react-hot-toast";
import { api } from "../axios";

export const ResetPassword = () => {
  const { token } = useParams();

  const navigate = useNavigate();

  return (
    <div className="reset-password-page-wrapper">
      <Toaster></Toaster>
      <div className="dark-themed-form reset-password-form-wrapper">
        <Formik
          initialValues={{ password: "", confirm_password: "" }}
          onSubmit={async (values) => {
            const errors = verifyResetPassword(values);
            console.error(values);
            if (errors.length == 0) {
              try {
                console.error(values);
                const { status } = await api.post(
                  `/user/reset-password`,
                  values,
                  {
                    params: { token },
                  }
                );
                if (status == 200) {
                  toast.success("Password successfully updated", {
                    onClose: () => navigate("/"),
                  });
                }
              } catch (e) {
                toast.error("Could not reset password");
              }
            } else {
              toast.error(errors[0]);
            }
          }}
        >
          {(formik) => {
            return (
              <form
                className="reset-password-form"
                onSubmit={formik.handleSubmit}
              >
                <div className="reset-password-form-title-wrapper">
                  <h4 className="form-title">Reset your password</h4>
                  <h4 className="form-subtitle">Make sure the two match</h4>
                </div>
                <div className="field">
                  <label htmlFor="password">Password</label>
                  <input
                    required={true}
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Password"
                    value={formik.values.password}
                    onChange={formik.handleChange}
                  />
                </div>
                <div className="field">
                  <label htmlFor="confirm-password">Confirm password</label>
                  <input
                    required={true}
                    type="password"
                    id="confirm-password"
                    name="confirm_password"
                    placeholder="Confirm your password"
                    value={formik.values.confirm_password}
                    onChange={formik.handleChange}
                  />
                </div>
                <button
                  className="reset-password-form-submit-button"
                  type="submit"
                >
                  Submit
                </button>
              </form>
            );
          }}
        </Formik>
      </div>
    </div>
  );
};
