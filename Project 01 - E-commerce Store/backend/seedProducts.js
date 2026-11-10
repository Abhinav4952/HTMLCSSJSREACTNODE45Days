
import mongoose from 'mongoose';
import 'dotenv/config';
import { Product } from './src/models/Product.js';

const products = [
    {
        name: 'Wireless Headphones',
        slug: 'wireless-headphones',
        description: 'Wireless headphones with clear sound and comfortable ear cushions.',
        priceCents: 7900,
        stock: 25,
        category: 'electronics'
    },
    {
        name: 'Smart Watch',
        slug: 'smart-watch',
        description: 'A smart watch with activity tracking and useful daily features.',
        priceCents: 5999,
        stock: 15,
        category: 'electronics'
    },
    {
        name: 'Bluetooth Speaker',
        slug: 'bluetooth-speaker',
        description: 'A portable Bluetooth speaker with powerful sound for everyday use.',
        priceCents: 3499,
        stock: 20,
        category: 'electronics'
    },
    {
        name: 'Cotton T-Shirt',
        slug: 'cotton-t-shirt',
        description: 'A comfortable cotton T-shirt suitable for casual everyday wear.',
        priceCents: 999,
        stock: 40,
        category: 'clothing'
    },
    {
        name: 'Denim Jeans',
        slug: 'denim-jeans',
        description: 'Classic denim jeans designed for comfortable everyday styling.',
        priceCents: 2499,
        stock: 18,
        category: 'clothing'
    },
    {
        name: 'Casual Hoodie',
        slug: 'casual-hoodie',
        description: 'A soft casual hoodie that provides warmth and comfort.',
        priceCents: 1999,
        stock: 22,
        category: 'clothing'
    },
    {
        name: 'Table Lamp',
        slug: 'table-lamp',
        description: 'A simple table lamp suitable for bedrooms and study tables.',
        priceCents: 1599,
        stock: 12,
        category: 'home'
    },
    {
        name: 'Ceramic Coffee Mug',
        slug: 'ceramic-coffee-mug',
        description: 'A reusable ceramic coffee mug for your favourite hot beverages.',
        priceCents: 499,
        stock: 50,
        category: 'home'
    }
];

async function seedProducts() {
    try {
        await mongoose.connect(process.env.MONGO_URI);
        await Product.insertMany(products);
        console.log('Eight sample products added successfully.');
    } catch (error) {
        console.error(error.message);
    } finally {
        await mongoose.disconnect();
    }
}

seedProducts();
