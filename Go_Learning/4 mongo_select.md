# Learning and talking

* 复杂查询

## Chapter 4

#### 1. 数组嵌套对象

~~~~
{
    id: 100
    list: [
        item1: {
            key: 90,
            value: {
                id: 100,
                name: 205
            }
        }
    ]
}

sq := bson.D{
		{"id", 100},
		{"list", bson.M{
			"$elemMatch": bson.M{
				"key": 90,
				"value.name": 205
			},
		}},
	}
~~~~

#### 2. 数组嵌套数组

~~~~
{
    id: 100
    list: [
        item1: {
            key: 90,
            value: [{
                id: 100,
                name: 205
            }]
        }
    ]
}

sq := bson.D{
		{"id", 100},
		{"list", bson.M{
			"$elemMatch": bson.M{
				"key": 90,
				"value": bson.M{
					"$elemMatch": bson.M{
						"id":  100,
						"name": 205
					},
				},
			},
		}},
	}
~~~~


#### 3. 数组交集数组

~~~~
{
    id: 100
    list: [
        item1: {
            key: 90,
            value: [ 100, 200 ]
        }
    ]
}

sq := bson.D{
		{"id", 100},
		{"list", bson.M{
			"$elemMatch": bson.M{
				"key": 90,
				"value": bson.M{
					"$elemMatch": bson.M{
						"$in": [200, 300],
					},
				},
			},
		}},
	}
~~~~



#### 4.特殊符号查询

~~~~
	PatientNamePingyin = `\Q` + PatientNamePingyin
	q := bson.M{"name_pinyin": bson.M{"$regex": PatientNamePingyin, "$options": "$i"}}
	query = append(query, q)
	curPatient, err := dbPatient.Find(context.TODO(), bson.M{"$and": query})
~~~~

#### 5.忽略返回某些字段

~~~~
	op := &options.FindOptions{}
	op.Projection = bson.M{"rx_list.beam_list.cp_list": 0}
~~~~