export function errorHandler(err, _req, res, _next) {
  console.error(err);
  const status = err.statusCode || err.status || 500;
  res.status(status).json({
    error: err.code || 'internal_error',
    message: err.message || 'Unexpected server error',
  });
}
