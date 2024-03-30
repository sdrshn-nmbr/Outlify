async function upload(req, res) {
  const { data, error } = await supabase
    .storage
    .from('bucketName')
    .upload('file-name.jpg', req.file.buffer)
  res.json({ data, error })
}

function a() {
  return (
    <form
      action="/api/upload"
      method="post"
      encType="multipart/form-data"
    >
      <input type="file" name="file" />
      <button type="submit">Upload</button>
    </form>
  )
}
