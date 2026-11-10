import mongoose from 'mongoose'
const userSchema = new mongoose.Schema({
        name:{
            type:String,
            required:true,
            trim:true,
            minlength:3,
            maxlength:20
        },
        email:{
            type:String,
            required:true,
            trim:true,
            lowercase:true
        },
        passwordHash:{
            type:String,
            required:true,
            minlength:8
        },
        role:{
            type:String,
            enum:['customer','admin'],
            default:'customer'
        }
    },
    {timestamps : true}
)

export const User = mongoose.model('user',userSchema)