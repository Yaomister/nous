export const verifyRegister = (fields) => {
  const { username, password, email } = fields;
  const errors = [];
  const usernameVerify = verifyUsername(username);
  if (!usernameVerify.valid) errors.push(usernameVerify.error);
  const emailVerify = verifyEmail(email);
  if (!emailVerify.valid) errors.push(emailVerify.error);
  const passwordVerify = verifyPassword(password);
  if (!passwordVerify.valid) errors.push(passwordVerify.error);
  return errors;
};

export const verifyResetPassword = (fields) => {
  const { password, confirm_password: confirmPassword } = fields;

  const passwordVerify = verifyPassword(password);
  if (!passwordVerify.valid) {
    return [passwordVerify.error];
  }

  if (password != confirmPassword) {
    return ["Passwords do not match"];
  }
  return [];
};

const verifyUsername = (username) => {
  const validRegex = /^[A-Za-z0-9_]+$/;
  if (!username) return { valid: false, error: "Username cannot be empty" };
  if (username.length > 20) return { valid: false, error: "Username too long" };
  if (!validRegex.test(username))
    return {
      valid: false,
      error:
        "Only alphanumeric characters and underscores are allowed in username",
    };

  return { valid: true };
};

const verifyEmail = (email) => {
  if (!email) return { valid: false, error: "Email cannot be empy" };

  const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;

  if (!emailRegex.test(email) || email.includes(" "))
    return { valid: false, error: "Email is invalid" };

  return { valid: true };
};

const verifyPassword = (password) => {
  const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
  if (!password) return { valid: false, error: "Password cannot be empty" };

  if (!specialChars.test(password))
    return {
      valid: false,
      error: "Password must contain a special character",
    };

  if (password.length < 8)
    return {
      valid: false,
      error: "Password must be at least 8 characters long",
    };

  if (password.includes(" "))
    return { valid: false, error: "Password cannot include a space" };

  return { valid: true };
};
