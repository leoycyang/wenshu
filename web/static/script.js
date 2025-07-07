// script.js - base JavaScript file for Flask template

document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript loaded and ready.");
    
    // Example: simple alert trigger
    const header = document.querySelector('header h1');
    if (header) {
        header.addEventListener('click', () => {
            alert("You clicked the header!");
        });
    }
});

new Vue({
    el: '#app',
    delimiters: ['${', '}'],  // change from {{ }} to ${ }
    data: {
        allData: [],
        currentPage: 1,
        pageSize: 10,
        fulltext_pattern: '',
    },
    computed: {
        totalPages() {
            return Math.ceil(this.allData.length / this.pageSize);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.allData.slice(start, start + this.pageSize);
        }
    },
    methods: {
        search() {
            this.fetchData(this.fulltext_pattern);
        },
        fetchData(query = '') {
            let url = '/contents';
            if (query) {
                url += '?query=' + encodeURIComponent(query);
            }
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.allData = data;
                    console.log(data);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        goToPage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
        }
    },
    mounted() {
        this.fetchData();
    }
});
