const express=require('express');
const app=express();
const mongoose=require('mongoose');
const Vote=require('./models/vote');
const morgan=require('morgan');

app.set('view engine','ejs');
app.use(express.static('public'));
// use morgan to log requests to the console
app.use(morgan('dev'));


dbURL='mongodb+srv://hetav:hv@nodetuts.bxgat3p.mongodb.net/trial';
mongoose.connect(dbURL,{useNewUrlParser:true,useUnifiedTopology:true})
    .then((result)=>{
        console.log('Connected to DB');
        app.listen(3000);
    })

app.get('/',(req,res)=>{
    res.render('PostVote.ejs');
});

app.get('/vote-count',async (req,res)=>{
    console.log("here");
    try{
        const voteCount=await Vote.find({vote_id:'1'});
        console.log(voteCount[0]);
        const count=voteCount[0].count;
        res.status(200).json({count});
    }
    catch(err){
        res.status(500).json({message:err.message});
    }
});

app.post('/upvote',async (req,res)=>{
    try{
        const updated=await Vote.findOneAndUpdate({vote_id:1},{$inc:{count:1}},{returnOriginal: false});
        console.log("noew")
        console.log(updated)
        const count=updated.count;
        res.status(200).json({count});  
    }
    catch(err) {
        res.status(500).json({message:err.message});
    }
})

app.post('/downvote',async (req,res)=>{
    try{
        const updated=await Vote.findOneAndUpdate({vote_id:1},{$inc:{count:-1}},{returnOriginal: false});
        const count=updated.count;
        res.status(200).json({count});  
    }
    catch(err) {
        res.status(500).json({message:err.message});
    }
})
