import mongoose from 'mongoose';

const bookSchema = new mongoose.Schema({
  title: { type: String, required: true, trim: true },
});

export const Book = mongoose.models.Book || mongoose.model('Book', bookSchema);
