const errorHandler = {
  transform: (errorObject) => {
    let errorMsg = {
      message: errorObject.message,
      title: errorObject.name,
    };

    // check if response has payload for custom message
    if (
      errorObject.response &&
      errorObject.response.data &&
      errorObject.response.data.message
    ) {
      errorMsg.message = errorObject.response.data.message;
    }
    return errorMsg;
  },
};

export default errorHandler;
