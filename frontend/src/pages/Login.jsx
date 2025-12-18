import { useFormik } from "formik";

export const Login = () => {
  const formuk = useFormik({
    initialValues: {
      username: "",
      password: "",
    },
    validateOnBlur: false,
    validateOnChange: false,
  });
  return <div className="login-page-wrapper"></div>;
};
