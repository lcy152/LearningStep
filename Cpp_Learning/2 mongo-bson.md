# Learning and talking

* websocket

## Chapter 2

#### 1. bson数组

~~~~
mongo::BSONElement instance_hash_id = result.getField("instance_hash_id_list");
if (!instance_hash_id.eoo() && instance_hash_id.type() == mongo::Array)
{
    vector<mongo::BSONElement> hostPorts = instance_hash_id.Array();
    for (vector<mongo::BSONElement>::iterator it = hostPorts.begin(); it != hostPorts.end(); ++it)
    {
        string temp;
        it->Val(temp);
        pending_series->get_instance_hash_id_list().push_back(temp.c_str());
    }
}
~~~~

