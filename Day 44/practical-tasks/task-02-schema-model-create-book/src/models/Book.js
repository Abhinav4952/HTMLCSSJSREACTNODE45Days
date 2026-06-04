import mongoose from 'mongoose';

const bookSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    // TODO(Day44-task02): add `trim: true` so leading/trailing whitespace is removed before validation/persist.
  },
});

export const Book = mongoose.models.Book || mongoose.model('Book', bookSchema);
