function main(params) {
  return {
        include_docs: true,
        database:"dealerships",
        query:{
            selector: {
                st: {
                        $eq: params.state
                    }
                },
            fields: [
                    "id",
                    "city",
                    "state",
                    "st",      
                    "address",
                    "zip",
                    "lat",
                    "long",
	                "short_name",
	                "full_name",
                ],
            sort: [
                    {
                        st: "asc"
                    }
                ]
            }, 
        params: { },
  };
}