import mongoose from 'mongoose';

const noteSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    title: { type: String, required: true, trim: true },
    body: { type: String, default: '', trim: true },
  },
  { timestamps: true },
);

export const Note = mongoose.models.Note || mongoose.model('Note', noteSchema);
