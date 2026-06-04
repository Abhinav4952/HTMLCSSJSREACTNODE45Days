import mongoose from 'mongoose';

const bookSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: true,
      trim: true,
      // TODO(Day44-task04): enforce `minlength: 3` so titles like "ab" fail validation.
    },
  },
  {
    // TODO(Day44-task04): enable `{ timestamps: true }` so Mongoose manages `createdAt` / `updatedAt`.
  },
);

export const Book = mongoose.models.Book || mongoose.model('Book', bookSchema);
