
    // function setProductInfo(element) {
        
    //     const productId = element.getAttribute('data-id');
    //     const formActionTemplate = element.getAttribute('data-url');
    //     document.getElementById('modalProductImage').src = element.getAttribute('data-image');
    //     document.getElementById('modalProductName').innerText = element.getAttribute('data-name');
    //     let price = element.getAttribute('data-price');
    //     let formattedPrice = parseFloat(price).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    //     document.getElementById('modalProductPrice').innerText = formattedPrice + ' đ';
    //     // document.getElementById('modalProductPrice').innerText = element.getAttribute('data-price') + ' đ';
    //     document.getElementById('modalProductBrand').innerText = element.getAttribute('data-brand');
    //     document.getElementById('modalProductReleaseYear').innerText = element.getAttribute('data-release-year');
    //     document.getElementById('modalProductGender').innerText = element.getAttribute('data-gioi-tinh');
    //     document.getElementById('modalProductNhomhuong').innerText = element.getAttribute('data-nhom-huong');
    //     document.getElementById('modalProductHuongDau').innerText = element.getAttribute('data-huong-dau');
    //     document.getElementById('modalProductHuongGiua').innerText = element.getAttribute('data-huong-giua');
    //     document.getElementById('modalProductHuongCuoi').innerText = element.getAttribute('data-huong-cuoi');
    //     document.getElementById('modalProductPhongCach').innerText = element.getAttribute('data-phong-cach');
    //     document.getElementById('modalProductLuuHuong').innerText = element.getAttribute('data-luu-huong');
    //     document.getElementById('modalProductNongDo').innerText = element.getAttribute('data-nong-do');
    //     // Cập nhật action cho form
    //     const formAction = formActionTemplate.replace('0', productId);
    //     document.getElementById('modalProductForm').action = formAction;
    // }

    // function setProductInfo(element) {
    //     const productId = element.getAttribute('data-id');
    //     const formActionTemplate = element.getAttribute('data-url'); // Lấy mẫu URL từ thuộc tính dữ liệu
    
    //     // Kiểm tra giá trị của formActionTemplate
    //     console.log('Form Action Template:', formActionTemplate); // Thêm dòng này để kiểm tra
    
    //     document.getElementById('modalProductImage').src = element.getAttribute('data-image');
    //     document.getElementById('modalProductName').innerText = element.getAttribute('data-name');
    //     let price = element.getAttribute('data-price');
    //     let formattedPrice = parseFloat(price).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    //     document.getElementById('modalProductPrice').innerText = formattedPrice + ' đ';
    //     document.getElementById('modalProductBrand').innerText = element.getAttribute('data-brand');
    //     document.getElementById('modalProductReleaseYear').innerText = element.getAttribute('data-release-year');
    //     document.getElementById('modalProductGender').innerText = element.getAttribute('data-gioi-tinh');
    //     document.getElementById('modalProductNhomhuong').innerText = element.getAttribute('data-nhom-huong');
    //     document.getElementById('modalProductHuongDau').innerText = element.getAttribute('data-huong-dau');
    //     document.getElementById('modalProductHuongGiua').innerText = element.getAttribute('data-huong-giua');
    //     document.getElementById('modalProductHuongCuoi').innerText = element.getAttribute('data-huong-cuoi');
    //     document.getElementById('modalProductPhongCach').innerText = element.getAttribute('data-phong-cach');
    //     document.getElementById('modalProductLuuHuong').innerText = element.getAttribute('data-luu-huong');
    //     document.getElementById('modalProductNongDo').innerText = element.getAttribute('data-nong-do');
    
    //     // Cập nhật action cho form
    //     const formAction = formActionTemplate.replace('0', productId);
    //     document.getElementById('modalProductForm').action = formAction;
    // }