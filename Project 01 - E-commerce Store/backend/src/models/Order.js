import mongoose from 'mongoose'

const orderSchema = new mongoose.Schema({
        user:{
            type:mongoose.Schema.Types.ObjectId,
            required:true,
            ref:'User',
        },
        items:{
            type:[
                {
                    product:{
                        type: mongoose.Schema.Types.ObjectId,
                        ref:'Product'
                    },
                    name:{type:String,required:true},
                    unitPriceCents:{type:Number,required:true},
                    qty:{type:Number,required:true,min:1,validate:Number.isInteger}
                }
            ]
        },
        status:{
            type:String,
            required:true,
            enum:['pending','paid','shipped','cancelled'],
            default:'pending'
        },
        shipping:{
            fullName:{type:String,required:true},
            line1:{type:String,required:true},
            city:{type:String,required:true},
            postalCode:{type:String,required:true},
            country:{type:String,required:true}
        },
        totalCents:{
            type:Number,
            required:true,
            validate:{
                validator:function(value) { return value===this.items.reduce((sum,item)=>sum+item.unitPriceCents*item.qty,0)}
            }
        }
    },
    {timestamps : true}
);

orderSchema.index({user:1,createdAt:-1})
orderSchema.index({status:1})

export const Order = mongoose.model('order',orderSchema)