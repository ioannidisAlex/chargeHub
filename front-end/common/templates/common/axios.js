const postBtn = document.getElementById('post-btn');

const sendData = () => {
	axios.post(
		'http://localhost:8001/evcharge/api/admin/login/',
		{
		username: 'dimitris',
		password: '1234',
		}
	)
	.then(response => {
		console.log(response);
	})
	.catch(err => {
		console.log(err);
	});
};

postBtn.addEventListener('click', sendData);