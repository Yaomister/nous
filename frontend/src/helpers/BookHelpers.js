export const verifyLog = (fields) => {
  const { rating } = fields;
  if (rating == 0) {
    return ["Cannot rate a book 0 stars!"];
  }

  return [];
};
