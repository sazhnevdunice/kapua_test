import React, { Component } from 'react';
import SortableTree from 'react-sortable-tree';
import FileExplorerTheme from 'react-sortable-tree-theme-full-node-drag';
import 'react-sortable-tree/style.css'; // This only needs to be imported once in your app

export default class Tree extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.onClickAddNode = this.onClickAddNode.bind(this);
    
    this.state = {
      rawData: [],
      treeData: [],
      nameNode: ''
    };
  }

  async componentDidMount() {
    const data = await (await fetch('http://localhost:8000/trees/nodes/')).json();
    const tree = this.compileTree(data);
    console.log('componentDidMount tree', tree)
    this.setState({
      rawData: data,
      treeData: tree,
    })
  }

  compileTree(data) {
    const tree = {};
    for (let item of data) {
      item.title = item.name;
      if (item.parent == null) {
        if (tree[item.id] != null) tree[item.id] = {...tree[item.id], ...item};
        else tree[item.id] = item;
      } else {
        if (tree[item.parent] == null) tree[item.parent] = {};
        if (tree[item.parent].children == null) tree[item.parent].children = [item];
        else tree[item.parent].children.push(item);
        if (tree[item.id] != null) tree[item.id] = {...tree[item.id], ...item};
        else tree[item.id] = item;
      }
    }

    const treeArray = [];

    for (let [key, value] of Object.entries(tree)) {
        if (value.parent == null) treeArray.push(value);
    }

    return treeArray;
  }

  async moveNode({ treeData, node, nextParentNode, prevPath, prevTreeIndex, nextPath, nextTreeIndex }) {
    // console.log(treeData, '\n', node, '\n', nextParentNode, '\n', prevPath, '\n', prevTreeIndex, '\n', nextPath, '\n', nextTreeIndex)
    console.log('treeData', treeData)
    console.log('node', node)
    console.log('nextParentNode', nextParentNode)
    if (nextParentNode && nextParentNode.id) {
      await (await fetch('http://localhost:8000/trees/move', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
          node_id: node.id,
          target_id: nextParentNode.id
        })
      }));
    }
  }

  handleChange(event) {
    const target = event.target,
    name = target.name,
    value = target.value;

    this.setState({
      [name]: value
    })
  }

  async onClickAddNode() {
    const {nameNode, rawData} = this.state;
    const rootId = 6;

    if (nameNode) {
      // Create new node
      const data = await (await fetch(`http://localhost:8000/trees/${rootId}/subtree/`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
          "name": nameNode,
          "parent": null
      })
      })).json();

      if (data) {
        rawData.push(data)
        const tree = this.compileTree(rawData);
        this.setState({
          rawData,
          treeData: tree,
          nameNode: '',
        })
      }
    } else {
       alert('Please enter name node!')
    }
  }

  render() {
    const {nameNode} = this.state;

    return (
      <div className="main-wrapper">
        <div style={{ height: 800 }}>
          <SortableTree
            treeData={this.state.treeData}
            onChange={treeData => this.setState({ treeData })}
            onMoveNode={this.moveNode.bind(this)}
            getNodeKey={({node, treeIndex}) => node.id}
            theme={FileExplorerTheme}
          />
        </div>
        <input name="nameNode" value={nameNode} onChange={this.handleChange} />
        <button onClick={this.onClickAddNode}>
          Add node
        </button>
      </div>
    );
  }
}