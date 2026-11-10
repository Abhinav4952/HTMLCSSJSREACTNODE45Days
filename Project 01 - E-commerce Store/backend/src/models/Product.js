import mongoose from 'mongoose'
const productSchema = new mongoose.Schema({
        name:{
            type:String,
            required:true,
            trim:true,
        },
        slug:{
            type:String,
            required:true,
            unique:true,
            lowercase:true
        },
        description:{
            type:String,
            required:true,
            minlength:20
        },
        priceCents:{
            type:Number,
            required:true,
            min:0,
            validate:Number.isInteger,
        },
        stock:{
            type:Number,
            required:true,
            min:0,
            validate:Number.isInteger
        },
        category:{
            type:String,
            enum:['electronics','clothing','home'],
            required:true
        },
        imageUrl:{
            type:String,
            default:'No Image Available'
        },
        isActive:{
            type:Boolean,
            default:true
        },
    },
    {timestamps : true}
);

productSchema.index({category:1})
productSchema.index({name:"text"})

export const Product = mongoose.model('product',productSchema)