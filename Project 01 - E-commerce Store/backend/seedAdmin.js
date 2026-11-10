import mongoose from "mongoose";
import 'dotenv/config';
import { User } from "./src/models/User.js";

const admin = {
    name : 'Admin',
    email:'admin@gmail.com',
    passwordHash:'admin@123',
    role:'admin'
}

async function seedAdmin() {
    try{
        await mongoose.connect(process.env.MONGO_URI);
        await User.insertOne(admin);
        console.log('Admin added successfully.');
    } catch(err){
        console.log(err.message);
    } finally {
        await mongoose.disconnect();
    }
}

seedAdmin();