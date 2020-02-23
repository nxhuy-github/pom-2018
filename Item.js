class Item{
    constructor(id, motif, coverage, pos_cov, neg_cov, length, items, area, like){
        this.id = id;
        this.motif = motif;
        //this.cover = cover;
        this.coverage = coverage;
        this.pos_cov = pos_cov;
        this.neg_cov = neg_cov;
        //this.obj_quality = obj_quality;
        this.length = length;
        this.items = items;
        this.area = area;
        this.like = like;
    }

    likeItem(){
        this.like++;
    }

    dislikeItem(){
        this.like--;
    }
}

module.exports = Item;