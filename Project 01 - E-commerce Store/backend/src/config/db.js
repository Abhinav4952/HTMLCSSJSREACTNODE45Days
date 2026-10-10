import mongoose from 'mongoose';

/**
 * Connect to MongoDB using MONGO_URI from .env.
 * Replace the placeholder in .env with your Atlas connection string before running `npm start`.
 * Format:
 * mongodb+srv://<username>:<password>@<cluster-host>/<database-name>?retryWrites=true&w=majority
 */
const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('MongoDB Connection Success 👍');
  } catch (error) {
    console.log('MongoDB Connection Failed 💥');
    console.error(error.message);
    process.exit(1);
  }
};

export default connectDB;
